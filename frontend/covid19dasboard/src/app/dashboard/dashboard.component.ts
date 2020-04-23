import { Component, OnInit, AfterViewInit, ElementRef, ViewChild,EventEmitter,Output} from '@angular/core';
import { ApiService } from '../app-service';
import { reduce } from 'rxjs/operators';
import { Observable } from 'rxjs/Observable';
import { shareReplay, map } from 'rxjs/operators';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';
import { environment } from '../../environments/environment'


@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css'],
})
export class DashboardComponent implements OnInit,AfterViewInit {

  api_data =  new Array(["Country", "Confirmed", "Recovered", "Death"]); // = ["Country", "Confirmed", "Recovered", "Death"]];
  key_data = new Array(["Country", "Confirmed","Recovered", "Death"]);
  @ViewChild('mapChart') mapChart: ElementRef
  private data$: Observable<any>;

readonly token =  environment.mapsApiKey;
  constructor(private apiService: ApiService) { }

  async ngOnInit() {
this.data$ = this.apiService.data;


this.data$.subscribe((data: any)=>{

  for (let item of data){
  this.key_data.push([item[0], item[0] + ": Confirmed:" +item[1], item[3], item[2]])
        }

      })
      //console.log(this.key_data)
      await new Promise(resolve => setTimeout(resolve, 1000))
        }


 drawChart = () => {


          const data =  google.visualization.arrayToDataTable(
       this.key_data
        );

        const options = {

          colors: ['blue']
            };

            const chart = new google.visualization.GeoChart(this.mapChart.nativeElement);
            chart.draw(data, options);


        }
        async ngAfterViewInit() {

              google.charts.load('current', { 'packages': ['geochart'], 'mapsApiKey': this.token });
              await new Promise(resolve => setTimeout(resolve, 10000));
              google.charts.setOnLoadCallback(this.drawChart);
            }



}
