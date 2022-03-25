import React from "react";
import { useParams } from "react-router-dom";
import Eventos from "../components/Eventos";

export default function Programacao(){
    // Pega os parâmetros passados na URL
    let params = useParams();
    return(
        /* Passa o nome da igreja como uma propriedade. (props)*/
        <React.Fragment>       
            <Eventos igreja={params.igreja}/>
        </React.Fragment>
    );
}