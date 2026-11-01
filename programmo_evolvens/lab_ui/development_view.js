/* Derive display frames from recorded events. Does not execute organism code. */
(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.PEDevelopment = api;
})(typeof window === 'undefined' ? {} : window, function () {
  function frame(events, index) {
    const cells = [], links = [], rules = new Set();
    let feedback = null, value = null;
    const copy = object => JSON.parse(JSON.stringify(object));
    const cursor = Math.max(0, Math.min(events.length - 1, index));
    for (const event of events.slice(0, cursor + 1)) {
      if (event.event === 'initial') cells.push(...copy(event.cells));
      if (event.event === 'cell_created') cells.push(copy(event.cell));
      if (event.event === 'mechanism_expressed') {
        const cell = cells.find(cell => cell.id === event.cell);
        if (cell) cell.mechanisms.push(copy(event.mechanism));
      }
      if (event.event === 'link_created') links.push(copy(event.link));
      if (event.origin?.rule) rules.add(event.origin.rule);
      if (event.event === 'mechanism_executed') {
        const cell = cells.find(cell => cell.id === event.cell);
        if (cell) {
          cell.used_steps += event.nodes.length;
          cell.memory = copy(event.memory);
          cell.state = 'running';
          cell.last_output = event.output;
        }
      }
      if (event.event === 'cell_stopped') {
        const cell = cells.find(cell => cell.id === event.cell);
        if (cell) { cell.state = 'stopped'; cell.health = event.reason; }
      }
      if (event.event === 'function_checked') {
        feedback = event.feedback;
        value = event.delivered ? event.value : null;
        for (const cell of cells) if (cell.state === 'running') cell.state = 'idle';
      }
    }
    return {cells, links, firedRules: [...rules], feedback, value, event: events[cursor], cursor};
  }
  return {frame};
});
