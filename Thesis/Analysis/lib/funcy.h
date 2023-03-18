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

// This function computes the magnitued of a vector
float computeMomentumMag(float PxPx, float PyPy, float PzPz){
  float P2 = PxPx + PyPy + PzPz;
  return P2;
}


float* coup (
	     float Px1Px1, float Py1Py1, float Pz1Pz1, 
	     float Px2Px2, float Py2Py2, float Pz2Pz2, 
	     float Px1Px2, float Py1Py2, float Pz1Pz2 
){
  static float p[9];
  p[0] = Px1Px1;
  p[1] = Py1Py1;
  p[2] = Pz1Pz1;
  p[3] = Px2Px2;
  p[4] = Py2Py2;
  p[5] = Pz2Pz2;
  p[6] = Px1Px2;
  p[7] = Py1Py2;
  p[8] = Pz1Pz2;


    return p;
}


// This function computes the vale of (P1 + P2)^2
float computeMomentumTot(float vars[9]){

  // unpack the list and calculate the (P1 + P2)^2 individual terms
  float PP1 = 0;
  float PP2 = 0;
  float P1P2 = 0;

  for( int i = 0; i < 9; i++){
    if (i < 3)
      // first 3 elements of vars are Px1Px1, Py1Py1 Pz1Pz1
      PP1 = PP1 + vars[i];

    else if (i >= 3 && i < 6)
      // Next 3 elements of vars are Px2Px2, Py2Py2 Pz2Pz2
      PP2 = PP2 + vars[i];
    
    else if (i>=6)
      // Next 3 elements of vars are Px1Px2, Py1Py2 Pz1Pz2
      P1P2 = P1P2 + vars[i];
  }
    
  float Ptot = PP1 + PP2 + 2 * P1P2;
  return Ptot;
}

// This funtion calculates the sq root of (PxPx1 + PyPy1 + PzPz1)*(PxPx2+PyPy2+PzPz2) 
float computeProductsSQ(float vars[6]){

  float sum1 = 0;
  float sum2 = 0;
  float P1[3] = {vars[0], vars[1], vars[2]};
  float P2[3] = {vars[3], vars[4], vars[5]};

  for( int i = 0; i<3; i++ ){
    sum1 += P1[i];
    sum2 += P2[i];
  }
  
  float output = TMath::Sqrt(sum1*sum2);
  return output;
}


#endif

    

