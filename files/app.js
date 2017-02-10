'use strict';

var MyComponent = function MyComponent(props) {
  return React.createElement(
    'p',
    null,
    props.children
  );
};

ReactDOM.render(React.createElement(
  MyComponent,
  null,
  'My component'
), document.getElementById('app'));