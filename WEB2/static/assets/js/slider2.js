
var slider = tns({
	container: '.my-slider',
	items: 1, /*item은 총 돌아가는 사진 갯수*/
	responsive: { /*화면의 크기에 따라 다르게 움직이게함(반응형)*/
	640: {
	edgePadding: 20,
	gutter: 20,
	items: 4
	},
	700: {
        gutter: 30
		},
				 
	},
	nav:false,
controlsContainer:".my-controls"
});