import React, { Component } from 'react';
import { Segment, Dimmer, Loader, Grid, Image, Form, Input, Dropdown, GridColumn } from 'semantic-ui-react'
import moment from 'moment';
import HeaderContent from './Header';
import axios from "axios";
// import Neovis from "neovis.js/dist/neovis.js";
import { NeoVisComponent } from './NeoVis';

export default class Home extends Component {
    constructor(props) {
      super(props);
      this.state = {
        loading: false,
      };
    }

    componentDidMount = () => {
      // this.setState({})
    }

    renderGrid = () => {
      return (
        <div>
          <Grid columns={4} divided>
            <Grid.Row>
              <Grid.Column>
                *Insert graph here*
              </Grid.Column>
              <Grid.Column>
              <Form.Field inline>
                <label ><b>Path 1</b></label>
                <Input 
                  name="path1" 
                  style={{ marginLeft: "10px"}}
                  placeholder="Enter path"
                  // onChange={this.handleInputChange}
                  // value={this.state.negalias}
                />
              </Form.Field>
              <Form.Field inline style={{ marginTop: "10px"}}>
                <label ><b>Path 2</b></label>
                <Input 
                  name="path2" 
                  style={{ marginLeft: "10px"}}
                  placeholder="Enter path"
                  // onChange={this.handleInputChange}
                  // value={this.state.negalias}
                />
              </Form.Field>
              <Form.Field inline style={{ marginTop: "10px"}}>
                <label ><b>Path 3</b></label>
                <Input 
                  name="path3" 
                  style={{ marginLeft: "10px"}}
                  placeholder="Enter path"
                  // onChange={this.handleInputChange}
                  // value={this.state.negalias}
                />
              </Form.Field>
              </Grid.Column>
              <Grid.Column>
              <Form.Field inline >
                <label ><b>Rank 1</b></label>
                <Dropdown
                  name = 'rank 1'
                  placeholder='Select ranking'
                  multiple
                  selection
                  style={{ marginLeft: "10px"}}
                />
              </Form.Field>

              <Form.Field inline style={{ marginTop: "10px"}}>
                <label ><b>Rank 2</b></label>
                <Dropdown
                  name = 'rank 2'
                  placeholder='Select ranking'
                  multiple
                  selection
                  style={{ marginLeft: "10px"}}
                />
              </Form.Field>

              <Form.Field inline style={{ marginTop: "10px"}}>
                <label ><b>Rank 3</b></label>
                <Dropdown
                  multiple
                  selection
                  style={{ marginLeft: "10px"}}
                  name = 'rank 3'
                  placeholder='Select ranking'
                />
              </Form.Field>
              </Grid.Column>

              <GridColumn>
                <Form.Field inline >
                  <label ><b>Adjacency</b></label>
                  <Dropdown
                    name = 'adjacency'
                    placeholder='Select adjacency'
                    multiple
                    selection
                    style={{ marginLeft: "10px"}}
                  />
                </Form.Field>

                <Form.Field inline style={{ marginTop: "10px"}}>
                  <label ><b>Adjacency</b></label>
                  <Dropdown
                    name = 'adjacency'
                    placeholder='Select adjacency'
                    multiple
                    selection
                    style={{ marginLeft: "10px"}}
                  />
                </Form.Field>

                <Form.Field inline style={{ marginTop: "10px"}}>
                  <label ><b>Adjacency</b></label>
                  <Dropdown
                    multiple
                    selection
                    style={{ marginLeft: "10px"}}
                    name = 'adjacency'
                    placeholder='Select adjacency'
                  />
                </Form.Field>
              </GridColumn>
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
              <NeoVisComponent query={query1}/>
              <br />
              <NeoVisComponent query={query2}/>
              <br />
              <NeoVisComponent query={query3}/>
              <br />
              <NeoVisComponent query={query4}/>
            </div>
          )}
        </div>
      );
    }
}