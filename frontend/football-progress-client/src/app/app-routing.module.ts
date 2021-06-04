import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { PerspectivePlayersComponent } from './component/perspective-players/perspective-players.component';
import { WelcomeComponent } from './component/welcome/welcome.component';

const routes: Routes = [
  {path: '', component: WelcomeComponent},
  {path: 'perspective-players', component: PerspectivePlayersComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
