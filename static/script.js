let testVariable = 'empty';

const  button_test_write = document.getElementById('test_button_write');
const  button_test_read = document.getElementById('test_button_read');

if (button_test_write){
button_test_write.addEventListener('click', function(){
    testVariable = 'new Value'
    console.log('write value:', testVariable, ' to testVariable')
});
}



if (button_test_read){
    button_test_read.addEventListener('click', function(){
    console.log('testVariable value: ', testVariable)
});


}
