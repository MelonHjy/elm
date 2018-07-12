$(document).ready(function(){
	var account=document.getElementById("account")
	var isinstance=document.getElementById("isinstance")
	var passwd=document.getElementById("passwd")
	var check=document.getElementById("check")
	var different=document.getElementById("different")
	var btn=document.getElementById("btn")

	btn.onclick = function (event){
		if (isinstance.style.display == 'block'|different.style.display == 'block'){
			return false;
		}else{
			return true;
		};	
	}
	account.addEventListener('blur',function(){
		acc = this.value
		if (acc==''){
			isinstance.style.display = 'block';
			isinstance.innerHTML = '不能为空'
			isinstance.style.color = 'red';
			btn.style.backgroundColor = 'red'
		}
		else{
		$.post(
			'/checkaccount/',
			{'acc':acc,"csrfmiddlewaretoken":$("[name='csrfmiddlewaretoken']").val()},
			function(data){
				if (data.status=='error'){
					isinstance.style.display = 'block';
					isinstance.innerHTML = data.message;
					isinstance.style.color = 'red';
					btn.style.backgroundColor = 'red'
				}
				if (data.status=='success'){
					isinstance.style.display = 'none';
					isinstance.style.color = '#2395ff';
					btn.removeAttribute('style')
				}
			}
		)}
	},false)
	check.addEventListener('blur',function(){
		pass = passwd.value
		che = this.value
		if (pass!=che){
			different.style.display = 'block';
			btn.style.backgroundColor = 'red'
		}
		if (pass==che){
			different.style.display = 'none';
			btn.removeAttribute('style')
		}
	},false)
})