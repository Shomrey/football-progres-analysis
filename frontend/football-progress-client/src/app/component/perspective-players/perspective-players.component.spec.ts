import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PerspectivePlayersComponent } from './perspective-players.component';

describe('PerspectivePlayersComponent', () => {
  let component: PerspectivePlayersComponent;
  let fixture: ComponentFixture<PerspectivePlayersComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PerspectivePlayersComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PerspectivePlayersComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
