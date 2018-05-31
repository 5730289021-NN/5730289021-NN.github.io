import React from 'react'

const ItemList = (props) =>  {
    return (
    <ul>
        {
        props.todos.map((todo,index) => {
        return (
            <li key={index} onClick={(event)=>props.onRemoveTodo(index)}>
                {todo}    
            </li>
            );
        })
        }
    </ul>
    );
}
export default ItemList;