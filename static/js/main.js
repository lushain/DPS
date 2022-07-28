document.addEventListener('DOMContentLoaded', function() {

  const template = document.getElementById('dropdown')
  const container = document.createElement('div')
     container.appendChild(document.importNode(template.content, true))

  tippy('.register', {
    content: container.innerHTML,
    allowHTML: true,
    arrow: true,
    trigger: 'click', // mouseenter, click, focus; manual.
    placement: 'bottom-end',
    animation: 'shift-away-subtle',
    duration: [250, 200],
    theme: 'light', // requires CSS to work
    interactive: true,
  })
});
