$(document).ready(function(){
	var m = document.getElementById("menu")
	var e = document.getElementById("evaluate")
	var s = document.getElementById("shop")
	
	var menu = document.getElementsByClassName("menu")
	var evaluate = document.getElementsByClassName("evaluate")
	var shop = document.getElementsByClassName("shop")
	
	m.addEventListener('click', function(){
		m.style.fontWeight = 'bold'
		e.style.fontWeight = '100'
		s.style.fontWeight = '100'
		menu[0].style.display = 'flex'
		evaluate[0].style.display = 'none'
		shop[0].style.display = 'none'
	},false)
	e.addEventListener('click', function(){
		m.style.fontWeight = '100'
		e.style.fontWeight = 'bold'
		s.style.fontWeight = '100'
		menu[0].style.display = 'none'
		evaluate[0].style.display = 'block'
		shop[0].style.display = 'none'
	},false)
	s.addEventListener('click', function(){
		m.style.fontWeight = '100'
		e.style.fontWeight = '100'
		s.style.fontWeight = 'bold'
		menu[0].style.display = 'none'
		evaluate[0].style.display = 'none'
		shop[0].style.display = 'block'
	},false)
	
	var cartRemoves = document.getElementsByClassName("cart-remove")
	var cartAdds = document.getElementsByClassName("cart-add")
	var send = document.getElementById("send")
	var check = document.getElementById("check")
	var money =document.getElementById("money")
	
	for (var i=0;i<cartAdds.length;i++){
		cartAdd=cartAdds[i];
		cartAdd.addEventListener('click',function(){
			ga = this.getAttribute('ga');
			num = document.getElementById(ga);
			cartRemove=document.getElementById(ga+'remove');
			cartRemove.style.display = 'block';
			num.style.display = 'block';
//			all_money = money.innerHTML;
			send.style.display = 'none';
			check.style.display = 'block';
			$.post(
				'/checkout/',
				{'method':'add','ga': ga,"csrfmiddlewaretoken":$("[name='csrfmiddlewaretoken']").val()},
				function(data){
					num.innerHTML=data.num;
					money.innerHTML=data.money;
				}
			)
		},false)
	}
	for (var i=0;i<cartRemoves.length;i++){
		cartRemove=cartRemoves[i];
		cartRemove.addEventListener('click',function(){
			ga = this.getAttribute('ga');
			num = document.getElementById(ga);
			remove=document.getElementById(ga+'remove');
			if (num.innerHTML == '1'){
				remove.style.display = 'none';
				num.style.display = 'none';
			}
			all_money = money.innerHTML;
			$.post(
				'/checkout/',
				{'method':'remove','ga': ga,"csrfmiddlewaretoken":$("[name='csrfmiddlewaretoken']").val()},
				function(data){
					num.innerHTML=data.num
					money.innerHTML=data.money
					if(data.money=='0'){
						send.style.display = 'block';
						check.style.display = 'none';
					}
				}
			)
		},false)
	}
})

