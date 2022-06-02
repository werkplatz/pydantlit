import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"
import { ReactNode } from "react";
import { JsonEditor as Editor } from 'jsoneditor-react';

import 'jsoneditor-react/es/editor.min.css';
import './jsoneditor.streamlit.css';
import ace from 'brace';
import 'brace/mode/json';
import 'brace/theme/github';

import Form from "@rjsf/bootstrap-4";
import './bootstrap.streamlit.css';
import Ajv from 'ajv';


interface State {
  value: object
}

class JsonForm extends StreamlitComponentBase<State> {
  ajv: Ajv.Ajv;
  resizeObserver = new ResizeObserver((entries: ResizeObserverEntry[]) => {
    Streamlit.setFrameHeight(entries[0].contentRect.height + 20)
  })

  observeElement = (element: HTMLDivElement | null) => {
    if (element !== null)
      this.resizeObserver.observe(element)
    else
      this.resizeObserver.disconnect()
  }
  constructor(props) {
    super(props);
    this.ajv = new Ajv({
      allErrors: true,
      verbose: true,
      useDefaults: true
    }
    );
    this.state = {value: this.value};
  }

  public render = (): ReactNode => {
    
    const schema = this.props.args["schema"]
        
    let editor;
    
    if (this.form === 'jsonschema') {
      editor =
        <Form
          showErrorList={false}
          children={true}
          schema={schema}
          uiSchema={this.props["uiSchema"]}
          formData={this.state.value}
          onChange={this.onChange}
          liveValidate={true}
          omitExtraData={true}></Form>
    }
    else {
      editor = <Editor
        value={this.state.value}
        history={true}
        ace={ace}
        ajv={this.ajv}
        theme="ace/theme/github"
        schema={schema}
        onChange={this.onChange}
        allowedModes={[
          'tree',
          'text'
        ]}>
      </Editor>
    }
    return (
      <div ref={this.observeElement}>
        {editor}
      </div>
    )
  }

  private get form() {
    return this.props.args["form"] ?? 'jsonschema'
  }

  private get value() {
    return this.props.args["default"] ?? {}
  }

  private onChange = (data: object): void => {
    let value
    if (this.form === 'jsonschema') {
      if (data['errors'].length === 0) {
        value = data['formData'] ?? this.value
      }
    }
    else {
      value = data ?? this.value
    }
    this.setState({value: value},()=>{
    if (value !== null) {
      Streamlit.setComponentValue(value)
    }
  })
  }
};

export default withStreamlitConnection(JsonForm)
