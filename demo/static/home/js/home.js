$(document).ready(function(){
	setTimeout(function(){
		swiper1(),
		swiper2()
	},100)
})

function swiper1(){
	var mySwiper1 = new Swiper('#topSwiper',{
		directorie:'horizontal',
		loop: true,
		speed:500,
		autoplay:2000,
		pagination:'.swiper-pagination',
		control:true,
	});
}

function swiper2(){
	var mySwiper1 = new Swiper('#topMenu',{
		slidesPerView: 5,
		paginationClickable: true,
		spaceBetween: 2,
		loop: false,
	});
}