import React, {Component} from 'react';
import {API_URL} from '../constants/index.js'
import { List } from 'reactstrap';
import axios from "axios";

class Linha extends Component{

    constructor(props){
        super(props)
        this.state = {
            programacao : []
        };        
    }

    componentDidMount() {
        axios.get(API_URL).then(res => this.setState({programacao: res.data}))
        .catch(error => console.error(error));
    }

    render(){
        /*console.log(this.state.programacao.map(function(elemento){
            return elemento.data + ' ' + elemento.nome;
        }))*/
        

        return(
            <div>
                <List type="unstyled">
                    {this.state.programacao.map(function(programacao){
                        return <li> {programacao.data + ' ' + programacao.nome} </li>;
                    })}
                </List>
            </div>
        );
    }   
    
}

export default Linha;