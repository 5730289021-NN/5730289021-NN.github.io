import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

import FormField from './components/form-field';
import ItemList from './components/item-list';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {todos : []};
  }

  render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">Welcome to React</h1>
        </header>
        <FormField addTodoList={todo=>this.setState({todos:[...this.state.todos, todo]})}/>
        <ItemList todos={this.state.todos} onRemoveTodo={this.removeTodo}/>
      </div>
    );
  }

  removeTodo = (index) => {
    let todos = this.state.todos.slice();
    todos.splice(index, 1);
    this.setState({todos});
  }
}
//
export default App;
