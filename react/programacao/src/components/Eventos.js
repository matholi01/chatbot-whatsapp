import React, {Component} from 'react';
import axios from "axios";
import {List} from 'reactstrap'
import Chip from '@mui/material/Chip';

// Retorna todos os eventos da semana atual de uma igreja específica como uma div
function getProgramacao(programacao){

    return programacao.map(programacao_dia =>
        <div>
            <div className="dia-eventos">
               { programacao_dia.dia_semana + ' • ' + programacao_dia.dia + ' ' + programacao_dia.mes }
            </div>
            <div className='lista-eventos'>
                { programacao_dia.eventos.map(evento =>
                    <dt>{ evento.horario + ' • ' + evento.nome}</dt>
                )}
            </div>
           
        </div>
    )   
}

class Eventos extends Component{

    constructor(props){   
        super(props)  
        this.state = {
            // Eventos da programação
            programacao : [],
        };        
    }


    componentDidMount() {

        // URL da api 
        let api_url = "http://localhost:8000/api/programacao/" + this.props.igreja + "/";
        
        // Faz a requisição se seta o status com os dados da programação
        axios.get(api_url).then(res => this.setState({programacao: res.data}))
        .catch(error => console.error(error));
        /*axios.get(api_url).then(res => console.log(res.data))
        .catch(error => console.error(error))*/
    }

    render(){
        
        return(
            <div className="eventos">
                <dl>
                    {getProgramacao(this.state.programacao)}
                </dl>  
            </div>
        );
    }   
    
}

export default Eventos;