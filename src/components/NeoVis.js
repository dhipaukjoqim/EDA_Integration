import React, { Component } from "react";
import Neovis from "neovis.js/dist/neovis.js";
import { Segment, Dimmer, Loader } from "semantic-ui-react";

import { v1 as uuid } from "uuid";

export const getUUID = () => {
  return uuid().replace(/-/g, "");
};

export class NeoVisComponent extends Component {
  constructor(props) {
    super(props);

    console.log("props", props)

    this.state = {
      loading: true,
      query: this.props.query,
      id: getUUID()
    };
  }

  componentDidMount() {
    console.log("componentDidMount");
    const self = this;
    var viz = self.draw();
    viz.render();
    this.setState({
      loading: false
    })
  }

  draw = () => {
    const config = {
      container_id: this.state.id,
      server_url: "bolt://10.115.1.250:7687",
      server_user: "neo4j",
      server_password: "ace_KG_001",
      initial_cypher: this.props.query,
      labels: {
        "indication": {
          caption: "name",
          size: "pagerank",
          community: "1"
        },
        "company": {
          caption: "name",
          size: "pagerank",
          community: "2"
        },
        "drug": {
          caption: "name",
          size: "pagerank",
          community: "3"
        }
      },
      //experiment with multiple nodes
      //render dropdowns
      relationships: {
        
      },
    };
    var viz = new Neovis(config);
    console.log("viz", viz);
    return viz;
  }

  render() {
    console.log("render", this.state );
    const { loading, id } = this.state;
    const viz={
      width: '900px',
      height: '370px'
    }
    return (
      <div>
        <div id={id} style={viz}></div>
        {!loading && (
          <div
            style={{
              textAlign: "center",
              marginTop: 60,
              marginBottom: 100
            }}
          >
          </div>
        )}
        {/* {this.state.loading && (
          <Segment style={{ marginTop: '40px', height: '400px', marginRight: "50px"}}>
            <Dimmer active inverted>
              <Loader inverted content='Loading' />
            </Dimmer>
          </Segment>
        )} */}
      </div>
    );
  }
}
