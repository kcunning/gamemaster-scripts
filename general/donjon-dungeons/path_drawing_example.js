// This is just an example bit of code. It's what I want
// generate_paths.py to output.

// We can't create pages at the moment


on("ready", function() {
    var currentPageID = Campaign().get('playerpageid'),
    currentPage = getObj('page', currentPageID);
    
    
    createObj('path', {
    stroke: '#ff0000',
        layer: 'objects',
        pageid: currentPageID,
        top: 70,
        left: 70,
        width: 140,
        height: 140,
        _path: JSON.stringify([
            ['M', 0, 0],
            ['L', 140, 0],
            ['L', 140, 140],
            ['L', 0, 140],
            ['L', 0, 0]
        ])
    });
})