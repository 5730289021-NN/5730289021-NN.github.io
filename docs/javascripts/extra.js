document.getElementsByClassName('md-header__title')[0].onclick = function() { location.href = document.location.origin }

var head = document.getElementsByTagName('head')[0];
[
  { httpEquiv: 'cache-control', content: 'no-cache, must-revalidate, post-check=0, pre-check=0' },
  { httpEquiv: 'cache-control', content: 'max-age=0' },
  { httpEquiv: 'expires', content: '0' },
  { httpEquiv: 'expires', content: 'Tue, 01 Jan 1980 1:00:00 GMT' },
  { httpEquiv: 'pragma', content: 'no-cache' }
].forEach(metaData => {
  var meta = document.createElement('meta');
  meta.httpEquiv = metaData.httpEquiv;
  meta.content = metaData.content;
  head.appendChild(meta);
});