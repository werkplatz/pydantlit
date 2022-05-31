import json
import os
import pydantic
import streamlit.components.v1 as components


# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
# (This is, of course, optional - there are innumerable ways to manage your
# release process.)
_RELEASE = False

# Declare a Streamlit component. `declare_component` returns a function
# that is used to create instances of the component. We're naming this
# function "_component_func", with an underscore prefix, because we don't want
# to expose it directly to users. Instead, we will create a custom wrapper
# function, below, that will serve as our component's public API.

# It's worth noting that this call to `declare_component` is the
# *only thing* you need to do to create the binding between Streamlit and
# your component frontend. Everything else we do in this file is simply a
# best practice.

if not _RELEASE:
    _component_func = components.declare_component(
        # We give the component a simple, descriptive name ("my_component"
        # does not fit this bill, so please choose something better for your
        # own component :)
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
        # via serialization to support custom serializers and special datatypes like datetime
        return value.parse_raw(json.dumps(form_value))
    except pydantic.ValidationError as e:
        return None

# app: `$ streamlit run pydantlit/__init__.py`
if not _RELEASE:
    import streamlit as st
    import glob
    import pathlib

    examples = pathlib.Path(__file__).parent.glob("example_*.py")    

    example = st.selectbox("Select example", map(lambda f: f.name[:-3], examples),index=1)
    module = __import__(example,fromlist=['__model__'])
    __model__: pydantic.BaseModel = getattr(module,'__model__')()
    __ui_schema__ = {}
    if hasattr(module,'__ui_schema__'):
        __ui_schema__ = getattr(module,'__ui_schema__')

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

    with st.form("ace"):
        value = pydantic_form(name="abc",
            value=__model__,
            form='ace')
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.json(value.dict())
