import React from 'react';
import { Container } from '@plone/components';
import Info from './Info';

/**
 * Component to display the footer.
 * @function Footer
 * @returns {string} Markup of the component
 */
const Footer = () => {
  return (
    <footer id="footer">
      <Container className="footer">
        <Info />
        <Container className="dados">Olá, pessoal!!</Container>
      </Container>
    </footer>
  );
};

export default Footer;
