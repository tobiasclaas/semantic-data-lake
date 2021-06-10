import React from 'react';

class Query extends React.Component {

    state = {
        databasename: "test",
        querystring: "select * where {?s ?p ?o .} LIMIT 25",
        graphname: "pizza",
        results: {
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
    
      Send = (props) => {
    
        var myHeaders = new Headers();
        myHeaders.append("Content-Type", "application/json");
        console.log("PROPS",props)
        var configs = {
          method: 'POST',
          headers: myHeaders,
          body: JSON.stringify(props),
          redirect: 'follow'
        };
        console.log("CONFIGS",configs)
        fetch("/fuseki", configs)
          .then(response => response.text())
          .then(result => {
            if (result.status >= 400) {
              throw new Error("Bad response from server");
            }
            this.setState({
              results: JSON.parse(result).results,
          })
          })
          .catch(error => console.log('error', error));
      };
    
      add = (e) => {
        e.preventDefault();
        if (this.state.querystring === "" || this.state.graphname === "") {
          alert("Both fields are mandatory!");
          return;
        }
        this.props.addQueryHandler(this.state);
        this.Send(this.state)
    
    
        this.setState({ querystring: "", graphname: "" });
      }
    
      render() {
        var data = this.state.results;
    
        return (
          <div>
            <h2>Pass a Query and specify which graph </h2>
            <form onSubmit={this.add}>
              <div>
                <label>Query </label>
                <input
                  type="text"
                  name="name"
                  placeholder="Querystring"
                  value={this.state.querystring}
                  onChange={(e) => this.setState({ querystring: e.target.value })}
                />
              </div>
              <div>
                <label>GraphName </label>
                <input
                  type="text"
                  name="email"
                  placeholder="GraphName"
                  value={this.state.graphname}
                  onChange={(e) => this.setState({ graphname: e.target.value })}
                />
              </div>
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
export default Query;