import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ClosestPlayersComponent } from './closest-players.component';

describe('ClosestPlayersComponent', () => {
  let component: ClosestPlayersComponent;
  let fixture: ComponentFixture<ClosestPlayersComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ClosestPlayersComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ClosestPlayersComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
