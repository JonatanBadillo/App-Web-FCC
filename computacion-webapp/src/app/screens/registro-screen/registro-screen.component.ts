import { Component } from '@angular/core';
import { MatRadioChange } from '@angular/material/radio';

@Component({
  selector: 'app-registro-screen',
  templateUrl: './registro-screen.component.html',
  styleUrls: ['./registro-screen.component.scss']
})
export class RegistroScreenComponent {
  public tipo:string = "registro-usuarios";
  public user:any = {};

  public radioChange(event:MatRadioChange){
    
  }

}
