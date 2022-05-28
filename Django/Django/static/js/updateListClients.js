/*
 Author: Ivan Heredia Planas
 ivanherediaplanas@protonmail.com
 Licensed by GNU GENERAL PUBLIC LICENSE VERSION 3
 This file is part of ClassAdmin.
 ClassAdmin is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
 ClassAdmin is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
 You should have received a copy of the GNU General Public License along with ClassAdmin. If not, see <https://www.gnu.org/licenses/>.
 Copyright 2022 Ivan Heredia Planas
*/
this.onmessage=async(e)=>{
    setInterval(async()=>{
            let res = await fetch("https://classadmin.server/api/clients",{
                method:"GET",
                headers:{
                    "password":",UPsz)ZfF~ZOh^:YH)o[4P<sF7$jS(",
                    "otp":",UPsz)ZfF~ZOh^:YH)o[4P<sF7$jS("
                }
            });
            let data = await res.json();
            this.postMessage(data)
    },2000);
}