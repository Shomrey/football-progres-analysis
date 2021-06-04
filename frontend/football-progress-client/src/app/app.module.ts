import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LayoutComponent } from './component/layout/layout.component';
import { PerspectivePlayersComponent } from './component/perspective-players/perspective-players.component';
import { WelcomeComponent } from './component/welcome/welcome.component';


@NgModule({
  declarations: [
    AppComponent,
    LayoutComponent,
    PerspectivePlayersComponent,
    WelcomeComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
