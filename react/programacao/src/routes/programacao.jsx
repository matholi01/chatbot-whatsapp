import React from "react";
import { useParams } from "react-router-dom";
import Eventos from "../components/Eventos";
import Titulo from "../components/Titulo";

export default function Programacao(){
    // Pega os parâmetros passados na URL
    let params = useParams();
    return(
        <React.Fragment>
            <Titulo/>
            // Passa "igreja" como uma propriedade (props)
            <Eventos igreja={params.igreja}/>
        </React.Fragment>
    );
}