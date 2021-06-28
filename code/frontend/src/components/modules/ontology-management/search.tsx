import React from 'react';
import workspacesStore from "../../../stores/workspaces.store";
import StoreStatus from "../../../models/storeStatus.enum";

class Search extends React.Component {

  constructor() {
    super();


    this.initialize();
  }

  private async initialize() {

    try {
      if (!workspacesStore.currentWorkspace)
        throw new Error("Current workspace must be set.");
      else{
        this.state.databasename = workspacesStore.currentWorkspace.id;
      }
    } catch (ex) {
      this.setStatus(StoreStatus.failed);
    }
  }

  Ok :boolean= false;

  state = {
    databasename: "test",
    querystring: "pizza",
    search: "True",
    results: {}
  }

  Send = (props) => {

    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    var configs = {
      method: 'POST',
      headers: myHeaders,
      body: JSON.stringify(props),
      redirect: 'follow'
    };
    
    fetch(`/workspaces/${workspacesStore.currentWorkspace.id}/ontologies`, configs)
      .then(response => response.text())
      .then(result => {
        if (result.status >= 400) {
          throw new Error("Bad response from server");
        }
        else{
          this.Ok = true;
        }
        this.setState({
          results: JSON.parse(result).results,
      })
      })
      .catch(error => console.log('error', error));
  };

  add = (e) => {
    e.preventDefault();
    if (this.state.querystring === "") {
      alert("Both fields are mandatory!");
      return;
    }
    this.props.addSearchHandler(this.state);
    this.Send(this.state)


    this.setState({ querystring: "", graphname: "" });
  }

  render() {
    
    if(this.Ok == true){
      var data = this.state.results;
    }
    else {
      var data = {
        "bindings": [
          {
            "s": {
              "type": "uri",
              "value": "http://www.co-ode.org/ontologies/ExampleOntology"
            },
            "p": {
              "type": "uri",
              "value": "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
            },
            "o": {
              "type": "uri",
              "value": "http://www.w3.org/2002/07/owl#Ontology"
            }
          }]
      }
    }

    

    return (
      <div>
        <h2>Pass a Keyword specify which graph </h2>
        <form onSubmit={this.add}>
          <div>
            <label>Query</label>
            <input
              type="text"
              name="name"
              placeholder="Keyword "
              value={this.state.querystring}
              onChange={(e) => this.setState({ querystring: e.target.value })}
            />
          </div>
{/*           <div>
            <label>GraphName</label>
            <input
              type="text"
              name="email"
              placeholder="GraphName "
              value={this.state.graphname}
              onChange={(e) => this.setState({ graphname: e.target.value })}
            />
          </div> */}
          <button>Send</button>
        </form>
        <table className="tat">
          <tr><th>Subject</th><th>Predicate</th><th>Object</th></tr>
          {
            data.bindings.map((dynamicData) =>
              <tr className="trow">
                <td>  {dynamicData.s.value}</td>
                <td> {dynamicData.p.value} </td>
                <td> {dynamicData.o.value} </td>
              </tr>
            )}
        </table>
      </div >
    )
  }
};
export default Search;