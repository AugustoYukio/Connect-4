import React, { useState } from "react";
import './SignIn.css';
import Card from "../../components/Card/Card";
import Input from "../../components/Input/Input";
import Button from "../../components/Button/Button";

export default () => {
    const [login, setLogin] = useState("");
    const [pwd, setPwd] = useState("");

    return (
        <div className='SignIn'>
            <Card title="Login" footerText="Novo por aqui?" linkUrl="/signup" textLink="Cadastre-se">
                <form>
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