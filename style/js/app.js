import 'bootstrap';
import Swal from 'sweetalert2';
import Plyr from 'plyr';
import {CountUp} from "countup.js";

window.onload = (t) => {
    window.axios = require('axios');
}
let player_error_page = document.getElementById('player');
if (player_error_page) {
    const player = new Plyr(player_error_page);
}
let clockd1_ = {
    "indicate": true,
    "indicate_color": "#222",
    "dial1_color": "#666600",
    "dial2_color": "#81812e",
    "dial3_color": "#9d9d5c",
    "time_add": 1,
    "time_24h": true,
    "date_add": 3,
    "date_add_color": "#999",
};

let credit = document.getElementById('credit');
if (credit) {
    credit.addEventListener('click', () => {
        Swal.fire({
            title: "สาสน์จากผู้พัฒนาเครื่องมือ Fujian",
            html: "<div style='text-align: left'>" +
                "ขอกราบขอบพระคุณศูนย์บริการการศึกษามหาวิทยาลัยเทคโนโลยีสุรนารี<br/>ในการให้บริการเว็บลงทะเบียนสำหรับนักศึกษาเป็นอย่างยิ่งนะครับ" +
                "<br/>เว็บไซต์นี้ถูกพัฒนาโดยผม ผู้ซึ่งเป็นอดีตนักศึกษา " +
                "สาขาวิชาเทคโนโลยีสารสนเทศ หลักสูตร ซอฟต์แวร์วิสาหกิจ มหาวิทยาลัยเทคโนโลยีสุรนารี</br>" +
                "ทางผู้พัฒนามิได้มีเจตนาปล่อยข้อมูลนักศึกษามหาวิทยาลัยเทคโนโลยีสู่สาธารณะ ข้อมูลทุกอย่าง จะถูก Obfuscate (ซ่อนซึ่งข้อมูลจริง) ก่อนการส่งออกจากระบบคอมพิวเตอร์ทุกครั้ง <br/>" +
                "</div>",
            icon: "info"
        });
    })
}
let countVal = document.getElementById('count').value;
if (countVal) {
    const countUp = new CountUp('counterDIV', parseInt(countVal));
    if (!countUp.error) {
        countUp.start();
    } else {
        console.error(countUp.error);
    }
}
