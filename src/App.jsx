import './App.css';
import Home from './pages/Home/Home';
import SignIn from './pages/SignIn/SingIn';
import SignUp from './pages/SignUp/SignUp';
import { BrowserRouter as Router, Route, Switch, Redirect } from 'react-router-dom';

function App() {
  return (
    <Router basename='/connect4'>
      <div className="App">
        <Switch>
          <Route path='/home'>
            <Home />
          </Route>
          <Route path='/signin'>
            <SignIn />
          </Route>
          <Route path='/signup'>
            <SignUp />
          </Route>
          <Route path="*">
            <Redirect to="/signin" />
          </Route>
        </Switch>
      </div>
    </Router>
  );
}

export default App;
