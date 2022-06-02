import json
import os
import pydantic
import streamlit.components.v1 as components


_RELEASE = os.environ.get('DEVELOP',None) is None  


if not _RELEASE:
    _component_func = components.declare_component(
        "pydantlit",
        # Pass `url` here to tell Streamlit that the component will be served
        # by the local dev server that you run via `npm run start`.
        # (This is useful while your component is in development.)
        url="http://localhost:3001",
    )
else:
    # When we're distributing a production version of the component, we'll
    # replace the `url` param with `path`, and point it to to the component's
    # build directory:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("pydantlit", path=build_dir)



def json_form(name,schema=None,default: pydantic.BaseModel=None,form=None, ui_schema=None):
    
    component_value = _component_func(name=name, schema=schema or {},
        default=default or {},
        form=form,
        ui_schema = ui_schema or {})
    return component_value

from pydantic import BaseModel

def pydantic_form(name,default: BaseModel=None,form=None,ui_schema=None):
    
    value_dict = {}
    if default:
        # via serialization to support custom serializers and special datatypes like datetime
        schema = default.schema()
        value_dict = json.loads(default.json())
    
    form_value = json_form(name = name,
        schema = schema or {},
        default=value_dict,
        form=form,
        ui_schema=ui_schema
    )
    try:
        return default.parse_raw(json.dumps(form_value))
    except pydantic.ValidationError as e:
        return None

# app: `$ streamlit run pydantlit/__init__.py`
if not _RELEASE:
    import streamlit as st
    import pathlib
    
    st.set_page_config(
        page_title='pydantlit demo',
        page_icon='https://assets.website-files.com/627944fe46fc8785fcad7040/627946067a4edda738e01318_logo.svg'
    )

    custom_json_name = 'custom_json'

    examples = pathlib.Path(__file__).parent.glob("example/*.py")    
    example = st.selectbox("Select example",
     ['custom_json_name'] + sorted(map(lambda f: f.name[:-3], examples)),index=1)
    
    
    schema = {}
    ui_schema = {}
    
    if example != custom_json_name:
        module = __import__(f'example.{example}', fromlist=['__model__'])
        model: pydantic.BaseModel = getattr(module,'__model__')()
        if hasattr(module,'__ui_schema__'):
            ui_schema = getattr(module,'__ui_schema__')
        schema = model.schema()

    
    if example in st.session_state:
        try:
            model= model.parse_raw(st.session_state[example])
        except pydantic.ValidationError:
            print(f'Invalid session state {example}. Falling back to default values.')

    with st.expander("Example code"):
        code = (pathlib.Path(__file__).parent / 'example'/ f"{example}.py").read_text()
        st.markdown(f"```python\n{code}\n```")
    with st.expander("See json schema"):
        st.json(model)
    if len(ui_schema)>0:
        with st.expander("See ui schema"):
            st.json(ui_schema)
    with st.expander("See input values"):
        st.text(model)
        st.json(model.parse_raw(model.json()).dict())

    with st.form("Json schema form",clear_on_submit=False):

        value = pydantic_form(name="json-schema-form", 
            default = model,
            form = 'jsonschema',
            ui_schema = ui_schema
            )
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.json(value.dict())
            st.session_state[example] = value.json()


    with st.form("Json editor",clear_on_submit=False):
        value = pydantic_form(name="json-editor",
            default = model,
            form='ace')
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.json(value.dict())
            st.session_state[example] = value.json()
            
