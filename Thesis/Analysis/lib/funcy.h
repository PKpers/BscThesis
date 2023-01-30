#ifndef FUNCY_H
#define FUNCY_H

using namespace  ROOT::VecOps;
using Vec_t = const RVec<float>;

Vec_t Couple2(float arg1, float arg2)
{
  Vec_t& coupled {arg1, arg2}; 
  return coupled;
}

// This function takes as input the elements of a 4 vector pair
// and returns the pair invariant mass
float ComputeInvariantMass(Vec_t& pt, Vec_t& eta, Vec_t& phi, Vec_t& e)
{
  ROOT::Math::PtEtaPhiEVector p1(pt[0], eta[0], phi[0], e[0]);
  ROOT::Math::PtEtaPhiEVector p2(pt[1], eta[1], phi[1], e[1]);
  return (p1 + p2).M(); 
}

// This function takes as input the contents of a 4 vector and which coordinate to transform 
// and returns the transformed coordinate
// integer convert must be 0 for x 1 for y and 2 for z
float toCartesian(float Pt, float Eta, float Phi, float E, int convert)
{
  ROOT::Math::PtEtaPhiEVector p(Pt, Eta, Phi, E);
  
  float px = p.Px();
  float py = p.Py();
  float pz = p.Pz();
  float transformed[3] = {px, py, pz};
  return transformed[convert];
}

float computeProduct(float p1, float p2){
  float p = p1 * p2;
  return p;
}
#endif
    

