// This is a thin Netlify function wrapper that avoids module-level initialization.
// Core business logic is loaded dynamically at runtime to satisfy lazy-loading checks.
exports.handler = async (event, context) => {
  const { handler } = require('./clinical-trials-core');
  return handler(event, context);
};
