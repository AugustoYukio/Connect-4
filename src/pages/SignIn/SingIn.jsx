import React, { useEffect, useState } from "react";
import { useHistory } from "react-router-dom";
import { useCookies } from 'react-cookie';
import './SignIn.css';
import Card from "../../components/Card/Card";
import Input from "../../components/Input/Input";
import Button from "../../components/Button/Button";
import Message from '../../components/Message/Message';

export default () => {
    const initialErrorState = {
        title: "Falha ao realizar login",
        errorList: []
    }

    let history = useHistory();
    
    const [cookies, setCookie] = useCookies(['name']);
    const [login, setLogin] = useState("");
    const [pwd, setPwd] = useState("");
    const [error, setError] = useState(initialErrorState);
    const [showError, setShowError] = useState(false);

    const isNullOrEmpty = array => {
        let string = array.trim();
        return string.length == 0 || string == null;
    }

    const addError = (errorList, e) => {
        if(errorList.indexOf(e) === -1) {
            errorList.push(e)
        }

        setError({ ...error, errorList });
    }

    const clearError = () => {
        setError(initialErrorState);
    }

    const validate = (user, password) => {
        let errors = [];
        
        if(isNullOrEmpty(user)) {
            addError(errors, "O campo usuário deve ser preenchido!");
        }

        if(isNullOrEmpty(password)) {
            addError(errors, "O campo senha deve ser preenchido!");
        }

        if(errors.length > 0){        
            return false;
        }
        
        let xhttp = new XMLHttpRequest();
        xhttp.open("POST", "http://127.0.0.1:5000/user/login", false);
        xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xhttp.send(JSON.stringify({"username": user, "password": password}));
        
        if(xhttp.status == 200){
            var json_response = JSON.parse(xhttp.responseText);
            var parsedJwt = parseJwt(json_response.token);
            setCookie('token', json_response.token, { path: '/' });
            setCookie('userID', parsedJwt.sub, { path: '/' });
            return true;
        }

        if(xhttp.status == 401){
            addError(errors, "Login e/ou Senha inválidos!");
            return false;
        }
    }

    const handleSubmit = async e => {

        e.preventDefault();
        clearError();        
        validate(login, pwd) ? history.push('/home') : history.push('/signin');
    }

    function parseJwt (token) {
        var base64Url = token.split('.')[1];
        var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        var jsonPayload = decodeURIComponent(window.atob(base64).split('').map(function(c) {
            return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
        }).join(''));
    
        return JSON.parse(jsonPayload);
    };

    useEffect(() => {
        setShowError(error.errorList.length > 0)
    }, [error])

    return (
        <div className='SignIn'>
            {showError && <Message onClose={clearError} msgTitle={error.title} msgInfo="Os seguintes erros foram detectados: " errorList={error.errorList} msgType="danger" /> }
            <Card title="Login" footerText="Novo por aqui?" linkUrl="/signup" textLink="Cadastre-se">
                <form onSubmit={handleSubmit}>
                    <div className="form-group my-5">
                        <Input 
                            inputName="usuario" 
                            label="Usuário" 
                            value={login} 
                            onChange={e => setLogin(e.target.value)} 
                        />
                        <Input 
                            inputType="password" 
                            inputName="senha" 
                            label="Senha" 
                            value={pwd} 
                            onChange={e => setPwd(e.target.value)}
                        />
                    </div>
                    <Button text="Acessar" type="submit" />
                </form>
            </Card>
        </div>
    )
}