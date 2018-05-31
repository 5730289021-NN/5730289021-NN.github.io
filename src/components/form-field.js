import React from 'react'


const FormField = props => {
    return (
        <div>
            <input id="form"/>
            <button onClick={()=>props.addTodoList(document.getElementById("form").value)}>Add</button>
        </div>
    );
}


export default FormField;