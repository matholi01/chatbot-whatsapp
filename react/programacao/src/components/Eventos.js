import React, {Component} from 'react';
import {API_URL} from '../constants/index.js'
import { Container, List } from 'reactstrap';
import axios from "axios";

function getProgramacao(programacao){
    return programacao.map(programacao_dia =>
        <div>
            <h2><b>{ programacao_dia.dia + ' ' + programacao_dia.mes}</b></h2>
            { programacao_dia.eventos.map(evento =>
                <li> { evento.horario + ' ' + evento.nome}</li>
            )}
        </div>
    )
    
}

class Eventos extends Component{

    constructor(props){
        super(props)
        this.state = {
            programacao : []
        };        
    }

    componentDidMount() {
        axios.get(API_URL).then(res => this.setState({programacao: res.data}))
        .catch(error => console.error(error));
        axios.get(API_URL).then(res => console.log(res.data))
        .catch(error => console.error(error))
    }

    render(){
        
        return(
            <div className="d-flex justify-content-center">
                <List type="unstyled">
                 {getProgramacao(this.state.programacao)}
                </List>
            </div>
        );
    }   
    
}

export default Eventos;