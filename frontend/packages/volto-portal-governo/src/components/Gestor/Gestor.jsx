import React from 'react';
import PropTypes from 'prop-types';
import { Container } from '@plone/components';

const Gestor = (props) => {
  const gestor = props.content.gestor;
  return (
    <Container narrow className={'gestor-wrapper'}>
      <h2>GESTOR</h2>
      {gestor && (
        <>
          {gestor.image_scales?.image && (
            <Container className={'image'}>
              <img
                src={`${gestor['@id']}/${gestor.image_scales.image[0].download}`}
              />
            </Container>
          )}

          <Container className="gestor-cargo">
            <h3 className={`gestor-nome}`}>{gestor.title}</h3>
          </Container>

          {gestor.description && (
            <Container className="gestor-biografia">
              <span>{gestor.description}</span>
            </Container>
          )}

          {gestor.cargo && (
            <Container className="gestor-cargo">
              <span>Cargo</span>: <span>{gestor.cargo.title}</span>
            </Container>
          )}
        </>
      )}
    </Container>
  );
};

export default Gestor;
