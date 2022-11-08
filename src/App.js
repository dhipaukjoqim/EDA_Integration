import React from 'react';
import Home from './components/Home';
import { Router, Route, Switch } from 'react-router-dom';
import history from '../src/history';

function App() {
  return (
    <>
      <Router history={history}>
        <Switch>
          <Route path="/" exact component={Home} />
        </Switch>
      </Router> 
    </>
  );
}

export default App;