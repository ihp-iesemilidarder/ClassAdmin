import {pageLogin} from './pageLogin.js'
import {pageDashboard} from './pageDashboard.js'
if(location.pathname=='/'){
    await pageLogin();
}else{
    await pageDashboard();
}