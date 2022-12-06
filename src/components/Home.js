import React, { Component } from 'react';
import { Segment, Dimmer, Loader, Grid, Button, Form, Input, Dropdown, Divider, Modal } from 'semantic-ui-react'
import moment from 'moment';
import HeaderContent from './Header';
import axios from "axios";
// import Neovis from "neovis.js/dist/neovis.js";
import { NeoVisComponent } from './NeoVis';
// const { request } = require('urllib');

export default class Home extends Component {
    constructor(props) {
      super(props);
      this.state = {
        loading: false,
        queries: [],
        rankOptions: [],
        adjacencyOptions: []
      };
    }

    componentDidMount = async() => {
      const queryString = window.location.search;
      console.log(queryString);

      const urlParams = new URLSearchParams(queryString);
      //console.log("urlParams", urlParams)


      // let response = await axios
      //   .post('http://localhost:5000/', this.state);
      //   console.log("response", response)

      const adjacencyOptions = [
        { key: 'adjacent', value: 'ADJACENT', text: 'ADJACENT' },
        { key: 'non-adjacent', value: 'NON-ADJACENT', text: 'NON-ADJACENT' }
      ]

      const rankOptions = [
        { key: '1', value: '1', text: '1' },
        { key: '2', value: '2', text: '2' },
        { key: '3', value: '3', text: '3' },
      ]

      this.setState({
        ...this.state,
        adjacencyOptions,
        rankOptions
      })
    }

    renderGrid = (q1, q2, q3, q4) => {
      return (
        <div>
          <Grid columns={3} divided>
            <Grid.Row>
              <Grid.Column>
                <Form.Field inline>
                {/* <label>Subgraph</label> */}
                <br />
                <Modal
                  trigger={<Button style={{marginLeft: "25%"}}>Show Subgraph</Button>}
                  header='Subgraph 1'
                  content={<NeoVisComponent query={q2}/>}
                  actions={['Close']}
                />
                
                </Form.Field>
                <br />

                <Form.Field>
                  <label style={{ marginLeft: "24px"}}><b>Path A</b></label>
                  <Input 
                    name="pathA" 
                    placeholder="Enter path"
                    // onChange={this.handleInputChange}
                    // value={this.state.negalias}
                    style={{ marginLeft: "10px"}}
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
                  />
                </Form.Field>
              </Grid.Column>
              <Grid.Column>
                <Form.Field inline>
                {/* <label>Subgraph</label> */}
                <br />
                <Modal
                  trigger={<Button style={{marginLeft: "25%"}}>Show Subgraph</Button>}
                  header='Subgraph 2'
                  content={<NeoVisComponent query={q3}/>}
                  actions={['Close']}
                />
                </Form.Field>
                <br />

                <Form.Field>
                  <label style={{ marginLeft: "24px"}}><b>Path B</b></label>
                  <Input 
                    name="pathB" 
                    placeholder="Enter path"
                    // onChange={this.handleInputChange}
                    // value={this.state.negalias}
                    style={{ marginLeft: "10px"}}
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
                  />
                </Form.Field>

                <br />
                <Form.Field inline>
                <label style={{marginTop: "10px"}}><b>Adjacency</b></label>
                  <Dropdown
                    name = 'adjacency'
                    placeholder='Select adjacency'
                    options={this.state.adjacencyOptions}
                    selection
                    style={{ marginLeft: "10px"}}
                  />
                </Form.Field>
              </Grid.Column>

              <Grid.Column>
                <Form.Field inline>
                {/* <label>Subgraph</label> */}
                <br />
                <Modal
                  trigger={<Button style={{marginLeft: "25%"}}>Show Subgraph</Button>}
                  header='Subgraph 3'
                  content={<NeoVisComponent query={q4}/>}
                  actions={['Close']}
                />
                </Form.Field>
                <br />

                <Form.Field>
                  <label style={{ marginLeft: "24px"}}><b>Path C</b></label>
                  <Input 
                    name="pathC" 
                    placeholder="Enter path"
                    // onChange={this.handleInputChange}
                    // value={this.state.negalias}
                    style={{ marginLeft: "10px"}}
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
                  />
                </Form.Field>

                <br />
                <Form.Field inline>
                <label style={{marginTop: "10px"}}><b>Adjacency</b></label>
                  <Dropdown
                    name = 'adjacency'
                    placeholder='Select adjacency'
                    options={this.state.adjacencyOptions}
                    selection
                    style={{ marginLeft: "10px"}}
                  />
                </Form.Field>
              </Grid.Column>
            </Grid.Row>
          </Grid>
        </div>
      )
    }

    render() {
      console.log("state in Home", this.state)
      let query1 = `match (n:indication) - [r1] - (x:drug) - [r2] - (y:company) - [r3] - (z:indication) return n,r1,x,r2,y,r3,z limit 3`

      let query2 = `MATCH (p) where p.name IN ['Endometriosis', 'Myovant Sciences Inc', 'Hormone dependent prostate cancer', 'prostate cancer'] or p.rdfs__label in ['Endometriosis', 'Myovant Sciences Inc', 'Hormone dependent prostate cancer', 'prostate cancer'] 
      with collect(id(p)) as nodes 
      CALL apoc.algo.cover(nodes) 
      YIELD rel 
      RETURN startNode(rel), rel, endNode(rel);`

      let query3 = `MATCH (p) where p.name IN ['Endometriosis', "Ardana to develop Zentaris' macimorelin and Teverelix ", 'Prostate tumor', 'prostate cancer'] or p.rdfs__label in ['Endometriosis', "Ardana to develop Zentaris' macimorelin and Teverelix ", 'Prostate tumor', 'prostate cancer'] 
      with collect(id(p)) as nodes 
      CALL apoc.algo.cover(nodes) 
      YIELD rel 
      RETURN startNode(rel), rel, endNode(rel);`

      let query4 = `MATCH (p) where p.name IN ['Endometriosis', 'relugolix', 'Prostate tumor', 'prostate cancer'] or p.rdfs__label in ['Endometriosis', 'relugolix', 'Prostate tumor', 'prostate cancer'] 
      with collect(id(p)) as nodes 
      CALL apoc.algo.cover(nodes) 
      YIELD rel 
      RETURN startNode(rel), rel, endNode(rel);`
      return (
        <div style={{ marginLeft: "50px", alignItems: "center"  }}>
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
              {this.renderGrid(query1, query2, query3, query4)}
              <br/>

              <Divider style={{marginTop: "30px"}}/>
              <div style={{ marginTop: "30px", marginBottom: "50px"}}>
                <h3>Parent graph</h3>
                <NeoVisComponent query={query1}/>
              </div>
            </div>
          )}
        </div>
      );
    }
}