import React, { useEffect, useState } from "react";
import './SignUp.css';
import Card from "../../components/Card/Card";
import Input from "../../components/Input/Input";
import Button from "../../components/Button/Button";
import Message from '../../components/Message/Message';

export default () => {
    const initialErrorState = {
        title: "Falha ao realizar cadastro",
        errorList: []
    }

    const [login, setLogin] = useState("");
    const [pwd, setPwd] = useState("");
    const [confirm, setConfirm] = useState("");

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

        if(isNullOrEmpty(confirm) || password !== confirm) {
            addError(errors, "As senhas nos campos 'Senha' e 'Confirmar senha' não batem!");
        }

        return errors.length == 0;
    }

    const handleSubmit = async e => {
        e.preventDefault();
        clearError();

        let result = validate(login, pwd);

        if(result) {
            console.log("Tudo certo!")
        } else {
            console.log("Ocorreu um erro!")
        }
    }

    useEffect(() => {
        setShowError(error.errorList.length > 0)
    }, [error])

    return (
        <div className='SignUp'>
            {showError && <Message onClose={clearError} msgTitle={error.title} msgInfo="Os seguintes erros foram detectados: " errorList={error.errorList} msgType="danger" /> }
            <Card title="Cadastro" footerText="Já possui cadastro?" linkUrl="/signin" textLink="Entrar">
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
                        <Input 
                            inputType="password" 
                            inputName="senha" 
                            label="Confirmar senha" 
                            value={confirm} 
                            onChange={e => setConfirm(e.target.value)}
                        />
                    </div>
                    <Button text="Cadastrar" type="submit" />
                </form>
            </Card>
        </div>
    )
}