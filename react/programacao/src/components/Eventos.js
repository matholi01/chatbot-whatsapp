import React, {Component} from 'react';
import axios from "axios";

// Retorna todos os eventos da semana atual de uma igreja específica como uma div
function getProgramacao(programacao){

    return programacao.map(programacao_dia =>
        <div>
            <div className="dia-eventos">
               { programacao_dia.dia_semana + ' • ' + programacao_dia.data }
            </div>
            <div className='lista-eventos'>
                { programacao_dia.eventos.map(evento =>
                    <dt className='evento'><b className='hora-eventos'>{ evento.horario }</b> •  { evento.nome}</dt>
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
            // Primeiro dia da semana, ou seja, a segunda daquela programação semanal
            primeiro_dia : "",
            // Último dia da semana, ou seja, o domingo daquela programação semanal
            ultimo_dia : "",
            // Nome da igreja daquela programação semanal
            igreja: ""
        };        
    }


    componentDidMount() {

        // URL da api 
        let api_url = "http://127.0.0.1:8000/api/programacao/" + this.props.igreja + "/";
        
        // Faz a requisição e seta o status com os dados da programação
        axios.get(api_url).then(res => this.setState({
            programacao: res.data.programacao, 
            primeiro_dia: res.data.primeiro_dia,
            ultimo_dia: res.data.ultimo_dia,
            igreja: res.data.igreja
        }))
        .catch(error => console.error(error));

        /*axios.get(api_url).then(res => console.log(res.data))
        .catch(error => console.error(error))*/

        // Deixa o fundo da cor desejada
        document.body.style.backgroundColor = "#1b1b1b"
    }

    render(){
        // Retorna todo o conteúdo da programação semanal
        return(
            <div className="conteudo">
                <div className="cabecalho">
                    <h1 className='titulo'>PROGRAMAÇÃO SEMANAL {'• ' + this.state.igreja}</h1>
                    <div className="info-cabecalho">
                        <h2 className='periodo'>{this.state.primeiro_dia + ' - ' + this.state.ultimo_dia}</h2>
                    </div>
                </div>
                <hr className="divisoria"></hr>
                <dl>
                    {getProgramacao(this.state.programacao)}
                </dl>  
            </div>
        );
    }   
    
}

export default Eventos;