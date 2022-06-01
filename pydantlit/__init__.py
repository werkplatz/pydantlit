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



def json_form(name,schema=None,value: pydantic.BaseModel=None,default=None,form=None, ui_schema=None):
    
    component_value = _component_func(name=name, schema=schema or {},
        value=value or {},
        default=default or {},
        form=form,
        ui_schema = ui_schema or {})
    return component_value

from pydantic import BaseModel

def pydantic_form(name,value: BaseModel,default=None,form=None,ui_schema=None):
    
    value_dict = {}
    if value:
        # via serialization to support custom serializers and special datatypes like datetime
        schema = value.schema()
        value_dict = json.loads(value.json())
    
    form_value = json_form(name = name,
        schema = schema or {},
        value = value_dict,
        default=default,
        form=form,
        ui_schema=ui_schema
    )
    try:
        return value.parse_raw(json.dumps(form_value))
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
    examples = pathlib.Path(__file__).parent.glob("example/*.py")    

    example = st.selectbox("Select example", sorted(map(lambda f: f.name[:-3], examples)),index=1)
    module = __import__(f'example.{example}',fromlist=['__model__'])
    __model__: pydantic.BaseModel = getattr(module,'__model__')()
    __ui_schema__ = {}
    

    if hasattr(module,'__ui_schema__'):
        __ui_schema__ = getattr(module,'__ui_schema__')

    input_path =  pathlib.Path(__file__).parent / '.data'/ f"{example}.json"
    input_path.parent.mkdir(exist_ok=True)
    if input_path.exists():
        try:
            __model__=__model__.parse_file(input_path)
        except pydantic.ValidationError:
            print(f'Invalid file {input_path}. Falling back to default values.')

    with st.expander("Example code"):
        code = (pathlib.Path(__file__).parent / 'example'/ f"{example}.py").read_text()
        st.markdown(f"```python\n{code}\n```")
    with st.expander("See json schema"):
        st.json(__model__.schema())
    if len(__ui_schema__)>0:
        with st.expander("See ui schema"):
            st.json(__ui_schema__)
    with st.expander("See input values"):
        st.text(__model__.json())
        st.json(__model__.parse_raw(__model__.json()).dict())

    with st.form("jsonschema"):
        value = pydantic_form(name="abc", 
            value = __model__,
            form = 'jsonschema',
            ui_schema = __ui_schema__
            )
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.json(value.dict())
            with input_path.open('w',encoding='utf-8') as f:
                f.write(value.json())

    with st.form("ace"):
        value = pydantic_form(name="abc",
            value=__model__,
            form='ace')
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.json(value.dict())
            with input_path.open('w',encoding='utf-8') as f:
                f.write(value.json())
