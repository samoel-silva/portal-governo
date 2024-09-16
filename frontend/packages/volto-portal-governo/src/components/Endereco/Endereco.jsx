import React from 'react';
import { Container } from '@plone/components';

const Endereco = (props) => {
  const { endereco, complemento, cidade, estado, cep } = props.content;
  return (
    <Container className="contato">
      <Container className="endereco">
        <span>Endereço</span>: <span>{endereco}</span>
      </Container>
      <Container className="endereco">
        <span>Complemento</span>: <span>{complemento}</span>
      </Container>
      <Container className="endereco">
        <span>Cidade</span>: <span>{cidade}</span>
        {estado && (
          <>
            - <span className="estado">{estado.token}</span>
          </>
        )}
      </Container>
      <Container className="endereco">
        <span>CEP</span>: <span>{cep}</span>
      </Container>
    </Container>
  );
};

export default Endereco;
