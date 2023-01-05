using namespace  ROOT::VecOps;
using Vec_t = const RVec<float>;
float ComputeInvariantMass(Vec_t& pt, Vec_t& eta, Vec_t& phi, Vec_t& M)
{
  ROOT::Math::PtEtaPhiMVector p1(pt[0], eta[0], phi[0], M[0]);
  ROOT::Math::PtEtaPhiMVector p2(pt[1], eta[1], phi[1], M[1]);
  return (p1 + p2).M(); 
}

Vec_t Couple2(float arg1, float arg2)
{
  Vec_t& coupled {arg1, arg2}; 
  return coupled;
}

float pt_sum(float pt0, float pt1)
{
  return pt0+pt1;
}

float pow_(float arg1, int arg2) //first argument will be the number and the second the power 
{
  int i;
  float result = 1;
  for (i=1; i<=arg2; i++) {
    result *= arg1;
  }
  return result;
}

float abs_(float arg1)
{
  float result;
  if(arg1 < 0){
    result = -arg1;
  }
  else{
    result = arg1;
  }
  return result;
}

float delta_ang(float ang1, float ang2)
{
  float pi = TMath::Pi();
  float delta_phi = abs_(ang2-ang1);
  if (delta_phi > pi){
    delta_phi = 2*pi - delta_phi;
  }
  return delta_phi;
}

float S_angle(float phi1, float phi2, float eta1, float eta2)
{
  float delta_phi = delta_ang(phi2, phi1);
  float delta_eta = delta_ang(eta2, eta1);
  float under_sqrt=pow_(delta_phi,2) + pow_(delta_eta, 2); 
  float sqrt_=sqrt(under_sqrt);
  return sqrt_;
}

float asign_mass(int flavor)
{
  float e_mass = 0.5/1000; //Gev
  float m_mass = 105.0/1000; //Gev
  float mass;
  if (flavor == 1){
    mass= e_mass;
  }
  if (flavor == 2){
    mass = m_mass;
  }
  return mass;
}

  
