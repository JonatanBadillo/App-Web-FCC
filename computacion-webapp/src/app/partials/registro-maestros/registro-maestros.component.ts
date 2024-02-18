import { Component, Input, OnInit } from '@angular/core';
import { MaestrosService } from '../../services/maestros.service';
declare var $:any;

@Component({
  selector: 'app-registro-maestros',
  templateUrl: './registro-maestros.component.html',
  styleUrls: ['./registro-maestros.component.scss']
})
export class RegistroMaestrosComponent implements OnInit{
  @Input() rol:string = "";

  public maestro:any = {};
  public editar:boolean = false;
  public errors:any = {};
  //Para contraseñas
  public hide_1: boolean = false;
  public hide_2: boolean = false;
  public inputType_1: string = 'password';
  public inputType_2: string = 'password';


  public areas:any[]= [
    {value: '1', viewValue: 'Desarrollo Web'},
    {value: '2', viewValue: 'Programacion'},
    {value: '3', viewValue: 'Base de Datos'},
    {value: '4', viewValue: 'Redes'},
    {value: '5', viewValue: 'Matematicas'},
  ];

  public materias:any[]= [
    {value: '1', nombre: 'Aplicaciones Web'},
    {value: '2', nombre: 'Programación 1'},
    {value: '3', nombre: 'Bases de datos'},
    {value: '4', nombre: 'Tecnologías Web'},
    {value: '5', nombre: 'Minería de datos'},
    {value: '6', nombre: 'Desarrollo móvil'},
    {value: '7', nombre: 'Estructuras de datos'},
    {value: '8', nombre: 'maestroistración de redes'},
    {value: '9', nombre: 'Ingeniería de Software'},
    {value: '10', nombre: 'maestroistración de S.O.'},
  ];

  constructor(
    private maestrosService: MaestrosService){}

  ngOnInit(): void {
    this.maestro = this.maestrosService.esquemaMaestro();
    this.maestro.rol = this.rol;
    console.log("maestro: ", this.maestro);
  }

  public regresar(){

  }

  public registrar(){
    //Validar
    this.errors = [];

    this.errors = this.maestrosService.validarMaestro(this.maestro, this.editar);
    if(!$.isEmptyObject(this.errors)){
      return false;
    }

    // TODO:Después registraremos admin
  }

  public actualizar(){

  }

//Funciones para password
showPassword()
{
  if(this.inputType_1 == 'password'){
    this.inputType_1 = 'text';
    this.hide_1 = true;
  }
  else{
    this.inputType_1 = 'password';
    this.hide_1 = false;
  }
}

showPwdConfirmar()
{
  if(this.inputType_2 == 'password'){
    this.inputType_2 = 'text';
    this.hide_2 = true;
  }
  else{
    this.inputType_2 = 'password';
    this.hide_2 = false;
  }
}

  public checkboxChange(event:any){
    //console.log("Evento: ", event);
    if(event.checked){
      this.maestro.materias_json.push(event.source.value)
    }else{
      console.log(event.source.value);
      this.maestro.materias_json.forEach((materia, i) => {
        if(materia == event.source.value){
          this.maestro.materias_json.splice(i,1)
        }
      });
    }
    console.log("Array materias: ", this.maestro);
  }


}
