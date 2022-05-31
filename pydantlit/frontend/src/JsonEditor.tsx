import {
    Streamlit,
    StreamlitComponentBase,
    withStreamlitConnection,
  } from "streamlit-component-lib"
import React, { ReactNode } from "react"
import { JsonEditor as Editor } from 'jsoneditor-react';
import 'jsoneditor-react/es/editor.min.css';
import ace from 'brace';
import 'brace/mode/json';
import 'brace/theme/github';

import {withTheme} from "@rjsf/core";

import { Theme } from "@rjsf/bootstrap-4";
import styled from 'styled-components';


import Ajv from 'ajv';

const ajv = new Ajv({ allErrors: true, verbose: true, useDefaults: true,discriminator: true});

const Form = withTheme(Theme);

interface State {
  isFocused: boolean
}


const Div = styled.div`
        .root {
        }
        .btn-primary {
          color: var(--text-color);
          background-color: var(--background-color);
          border-color: var(--secondary-background-color);
        }
        .btn-primary:hover {
          color: var(--primary-color);
          background-color: var(--background-color);
          border-color: var(--primary-color);
        }
        .btn-primary:focus {
          color: var(--primary-color);
          background-color: var(--background-color);
          border-color: var(--primary-color);
        }
        .custom-control-input:checked ~ .custom-control-label::before {
          color: var(--primary-color);
          background-color: var(--background-color);
          border-color: var(--primary-color);
        }
        .custom-switch
          .custom-control-input:disabled:checked
          ~ .custom-control-label::before {
            background-color: var(--background-color);
        }
        .dropdown-item.active,
        .dropdown-item:active {
          color: var(--primary-color);
          background-color: var(--background-color);
          border-color: var(--primary-color);
        }
        .form-control:focus {
          color: #495057;
          background-color: #fff;
          border-color: var(--primary-color);
          box-shadow: 0 0 0 0.2rem var(--primary-color);
        }
        .nav-pills .show > .nav-link {
          color: #fff;
          background-color: var(--primary-color);
        }
        .btn-primary:focus {
          color: #fff;
          background-color: var(--primary-color);
          border-color: var(--primary-color);
          box-shadow: 0 0 0 0.2rem var(--primary-color);
        }
        a {
          color: var(--primary-color);
        }
        a:hover {
          color: var(--primary-color);
        }
        .bg-primary {
          background-color: var(--primary-color);
        }
        .border-primary {
          border-color: var(--primary-color);
        }
        .text-primary {
            color:  var(--primary-color);
        }
        .list-group-item.active {
          z-index: 2;
          color: #fff;
          background-color: var(--primary-color);
          border-color: var(--primary-color);
        }
        .jsoneditor {
          color: var(--text-color);
          border: 0
        }
        .jsoneditor-menu > button {
          background-color: #000000;
        }
        .jsoneditor-menu {
          width: 100%;
          height: 35px;
          padding: 2px;
          margin: 0;
          box-sizing: border-box;
          color: var(--text-color);
          background-color: #000000;
          border-bottom: 1px solid var(--background-color);
      }
        `

class JsonEditor extends StreamlitComponentBase<State> {
    formRef: React.RefObject<HTMLDivElement>;
    constructor(props){
      super(props);
      this.formRef = React.createRef();
    }

    public render = (): ReactNode => {
      const schema = this.props.args["schema"]
      const resizeObserver = new ResizeObserver((entries: ResizeObserverEntry[]) => {
        Streamlit.setFrameHeight(entries[0].contentRect.height+20)
      })

      
      const observeElement = (element: HTMLDivElement | null) => {
        if (element !== null)
          resizeObserver.observe(element)
        else
          resizeObserver.disconnect()
      }

      Streamlit.setComponentValue(this.value)

      let editor;

      if(this.form === 'jsonschema'){
        editor = 
          <div ref = {this.formRef}>
          <Form id="jsonschema-form"
            children = {true}
            schema={schema}
            uiSchema = {this.props.args['ui_schema']}
            formData={this.props.args['value'] ?? {} }
            onChange={this.onChange}
            liveValidate={true}
            omitExtraData= {true}
          ></Form>
          </div>
      }
      else {
        editor = <Editor
        value={this.props.args['value'] ?? {} }
        history={true}
        ace={ace}
        ajv={ajv}
        theme="ace/theme/github"
        schema={schema}
        onChange={this.onChange}
        allowedModes={[
          'tree',
          'text'
        ]}></Editor>
      }
      return (
        <Div ref={observeElement}>
          {editor}
        </Div>
      )
    }
  
    private get form(){
      return this.props.args["form"] ?? 'jsonschema'
    }

    private get value(){
      return this.props.args["value"] ?? {}
    }

    private onBlur = (id: string,data: object): void => {
      // this.formRef.current.get
      this.onChange(data)
    }

    private onChange = (data: object): void => {
      let value
      if(this.form === 'jsonschema'){
      if(data['errors']?.length===0){
          value = data['formData'] ?? this.props.args["value"]
      }
      }
      else {
          value = data ?? this.props.args["value"] 
      }
      if(value!==null){
        Streamlit.setComponentValue(value)
      }
    }
  };
  
export default withStreamlitConnection(JsonEditor)
