import React from "react";
import CategoryGrid from "../components/CategoryGrid.js"
import "./Home.css"

// Contains divs of all the groups to be displayed

const Home = () => (
  <div>
    <div className="wrapper">
      <CategoryGrid group="Men"/>
    </div>
    <div className="wrapper">
      <CategoryGrid group="Women"/>
    </div>
  </div>
);

export default Home;
