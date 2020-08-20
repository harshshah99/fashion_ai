import React from 'react';
import './App.css';
import CardListTrending from './components/CardListTrending.js';
import CardListUpcoming from './components/CardListUpcoming.js';
import Home from './pages/Home'
import { BrowserRouter as Router, Route, Link } from "react-router-dom";

// Creates a fixed floating header along with a router to seperate the homepage and category pages
const App = () => (
  <Router>
    <div className="App">
      <header className="App-header">
        <Link className="textDecorator" to="/">Fashion Intelligent Systems</Link>
      </header>
      <hr />

      <Route exact path="/" component={Home} />
      <Route path="/category/Trending" component={CardListTrending} />
      <Route path="/category/Upcoming" component={CardListUpcoming} />
    </div>
  </Router>
);

export default App;