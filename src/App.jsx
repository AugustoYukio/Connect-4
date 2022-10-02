import './App.css';
import Menu from './pages/Menu/Menu';
import SignIn from './pages/SignIn/SingIn';
import SignUp from './pages/SignUp/SignUp';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';

function App() {
  return (
    <Router basename='/connect4'>
      <div className="App">
        <Switch>
          <Route exact path='/'>
            <Menu />
          </Route>
          <Route path='/signin'>
            <SignIn />
          </Route>
          <Route path='/signup'>
            <SignUp />
          </Route>
        </Switch>
      </div>
    </Router>
  );
}

export default App;
