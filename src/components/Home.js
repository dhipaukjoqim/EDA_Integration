import React, { Component } from 'react';
import { Segment, Dimmer, Loader, Grid, Button, Form, Input, Dropdown, Divider, Modal } from 'semantic-ui-react'
import moment from 'moment';
import HeaderContent from './Header';
import axios from "axios";
// import Neovis from "neovis.js/dist/neovis.js";
import { NeoVisComponent } from './NeoVis';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
// const { request } = require('urllib');

export default class Home extends Component {
    constructor(props) {
      super(props);
      this.state = {
        loading: false,
        queries: [],
        rankOptions: [],
        adjacencyOptions: [],
        rowCount: 0,
        documents: [],
        fullgraph: ''
      };
    }

    componentDidMount = async() => {
      const queryString = window.location.search;
      const adjacencyOptions = [
        { key: 'adjacent', value: 'ADJACENT', text: 'ADJACENT' },
        { key: 'non-adjacent', value: 'NON-ADJACENT', text: 'NON-ADJACENT' }
      ]
      
      let rowCount = queryString.split('=')[1];
      const rankOptions = this.prepareRankOptions(rowCount);

      this.setState({
        rowCount,
        adjacencyOptions,
        rankOptions,
      }, async() => {
        let response = await axios
        .post('http://localhost:5000/', this.state);
        console.log("response", response);

        this.setState({
          documents: response.data.documents,
          queries: response.data.subgraphs,
          fullgraph: response.data.fullgraph
        })
      })
    }

    prepareRankOptions = (rowCount) => {
      let rankOptionsArray = [];
      for(let i=0; i<rowCount; i++) {
        let object = {};
        object.key = i+1;
        object.value = i+1;
        object.text = i+1;

        rankOptionsArray.push(object)
      }

      return rankOptionsArray;
    }

    //Column "path" needs to be added in SQL table
    handleInputChange = (docId) => {
      let docs = this.state.documents;
      console.log("docId", docId);
    }

    handleDropdownChange = docId => (e, data) => {
      console.log(data.name, data.value, docId);
      let docs = this.state.documents;
      for(let i=0; i<docs.length; i++) {
        if(docs[i][0] == docId) {
          docs[i][3] = data.value
        }
      }

      this.setState({
        ...this.state,
        documents: docs
      });
    }

    handleAdjacencyDropdownChange = docId => (e, data) => {
      console.log(data.name, data.value, docId);
      let docs = this.state.documents;
      for(let i=0; i<docs.length; i++) {
        if(docs[i][0] == docId) {
          docs[i][4] = data.value
        }
      }

      this.setState({
        ...this.state,
        documents: docs
      });
    }

    renderGrid = () => {
      let queries = this.state.queries;
      console.log("queries", queries)
      return (
        <div>
          <Grid columns={this.state.documents.length} divided>
            <Grid.Row>
              {this.state.documents.map((doc, index) => {
                return (
                  <Grid.Column key={doc[0]}>
                    <Form.Field inline>
                    <br />
                    <Modal
                      trigger={<Button style={{marginLeft: "25%"}}>Show Subgraph</Button>}
                      header='Subgraph 1'
                      content={<NeoVisComponent query={queries[index]}/>}
                      actions={['Close']}
                    />
                    {/* {doc[0]} */}
                    </Form.Field>
                    <br />

                    <Form.Field>
                      <label style={{ marginLeft: "24px"}}><b>Path</b></label>
                      <Input 
                        name="pathA" 
                        placeholder="Enter path"
                        onChange={() => this.handleInputChange(doc[0])}
                        style={{ marginLeft: "22px"}}
                      />
                    </Form.Field>
                    <br />

                    <Form.Field inline>
                      <label style={{marginLeft: "22px"}}><b>Rank</b></label>
                      <Dropdown
                        name = 'rank'
                        placeholder='Select ranking'
                        selection
                        options={this.state.rankOptions}
                        style={{ marginLeft: "21px"}}
                        onChange={this.handleDropdownChange(doc[0])}
                        value={doc[3]}
                      />
                    </Form.Field>

                    <br />
                    <Form.Field inline>
                    <label style={{marginTop: "10px"}}><b>Adjacency</b></label>
                      <Dropdown
                        name = 'adjacency'
                        placeholder='Select adjacency'
                        selection
                        options={this.state.adjacencyOptions}
                        style={{ marginLeft: "10px"}}
                        onChange={this.handleAdjacencyDropdownChange(doc[0])}
                        value={doc[4]}
                      />
                    </Form.Field>
                  </Grid.Column>
                ) 
              })}
              
              
            </Grid.Row>
          </Grid>
        </div>
      )
    }

    handleUpdate = async() => {
      console.log("Inside handleUpdate")
      let response = await axios
        .post('http://localhost:5000/update', this.state);
      console.log("response", response);

      if(response.data.message == 'updated') {
        toast.success('Curations updated!', {
          position: "top-right",
          autoClose: 5000,
          hideProgressBar: false,
          closeOnClick: true,
          pauseOnHover: true,
          draggable: true,
          progress: undefined,
          theme: "light",
        });
      }
    }

    render() {
      console.log("state in Home", this.state);
      
      let fullgraph = this.state.fullgraph;
      console.log("fulraph", fullgraph)
      return (
        <div style={{ marginLeft: "50px", alignItems: "center"  }}>
          <ToastContainer />
          {this.state.loading && (
            <Segment style={{ marginTop: '40px', height: '400px', marginRight: "50px"}}>
              <Dimmer active inverted>
                <Loader inverted content='Loading' />
              </Dimmer>
            </Segment>
          )}
          {!this.state.loading && (
            <div style={{ marginRight: "100px"}}>
              
              <HeaderContent />
              <div style={{ marginTop: "30px"}}>
                <h3>Subgraphs</h3>
              </div>
              {this.state.documents.length>0 && this.renderGrid()}
              <br/>
              <Button primary onClick={this.handleUpdate}>Update</Button>

              <Divider style={{marginTop: "30px"}}/>
              {this.state.fullgraph && (
                <div style={{ marginTop: "30px", marginBottom: "50px"}}>
                  <h3>Parent graph</h3>
                  <NeoVisComponent query={fullgraph}/>
                </div>
              )}
              
            </div>
          )}
        </div>
      );
    }
}