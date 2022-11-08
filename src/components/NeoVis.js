import React, { Component } from "react";
import Neovis from "neovis.js/dist/neovis.js";

import { v1 as uuid } from "uuid";

export const getUUID = () => {
  return uuid().replace(/-/g, "");
};

export class NeoVisComponent extends Component {
  constructor(props) {
    super(props);

    this.state = {
      loading: true,
      query: props.query,
      id: getUUID()
    };
  }

  componentDidMount() {
    console.log("componentDidMount");
    const self = this;
    var viz = self.draw();
    viz.render();
  }

  draw = () => {
    const config = {
      container_id: this.state.id,
      server_url: "bolt://10.115.1.250:7687",
      server_user: "neo4j",
      server_password: "ace_KG_001",
      initial_cypher: this.state.query
    };
    var viz = new Neovis(config);
    console.log("viz", viz);
    return viz;
  }

  render() {
    console.log("render");
    const { loading, id } = this.state;
    return (
      <div>
        <div id={id}></div>
        {!loading && (
          <div
            style={{
              textAlign: "center",
              marginTop: 60,
              // width: "1000px",
              // height: "600px",
            }}
          >
          </div>
        )}
      </div>
    );
  }
}
