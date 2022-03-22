import React, {Component} from 'react';
import { List } from 'reactstrap';
import axios from "axios";


function getProgramacao(programacao){

    return programacao.map(programacao_dia =>
        <div>
            <h2>{ programacao_dia.dia_semana + ' • ' + programacao_dia.dia + ' ' + programacao_dia.mes}</h2>
            <div className='lista-eventos'>
                { programacao_dia.eventos.map(evento =>
                    <li> { evento.horario + ' • ' + evento.nome}</li>
                )}
            </div>
        </div>
    )   
}

class Eventos extends Component{

    constructor(props){   
        super(props)  
        this.state = {
            programacao : [],
        };        
    }


    componentDidMount() {

        let api_url = "http://localhost:8000/api/programacao/" + this.props.igreja + "/";
        
        axios.get(api_url).then(res => this.setState({programacao: res.data}))
        .catch(error => console.error(error));
        axios.get(api_url).then(res => console.log(res.data))
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